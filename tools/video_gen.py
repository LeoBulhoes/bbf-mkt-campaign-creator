"""
Video generation module — multi-provider.
Routes to Google Veo 3.1 (default) based on model/provider selection.

Mirrors image_gen.py's architecture:
- generate_video() — single video
- generate_for_record() — one Airtable record
- generate_batch() — batch with cost summary + parallel polling
"""

import time
from . import config
from .utils import print_status
from .gcp_upload import upload_references
from .airtable import update_record
from .providers import get_video_provider, is_sync


_MODEL_DISPLAY_NAMES = {
    "veo-3.1": "Veo 3.1",
    "kling-3.0": "Kling 3.0",
    "sora-2": "Sora 2",
    "sora-2-pro": "Sora 2 Pro",
}

# Reverse mapping: Airtable display name -> internal model name
_AIRTABLE_TO_INTERNAL = {v: k for k, v in _MODEL_DISPLAY_NAMES.items()}


def generate_video(prompt, image_urls=None,
                   aspect_ratio="9:16", duration="8", resolution="720p",
                   model=None, provider=None):
    """
    Generate a single video (submit + poll).

    Args:
        prompt: Video generation prompt
        image_urls: List of URLs. First is start frame, rest are anchors.
        aspect_ratio: "9:16" or "16:9"
        duration: "4", "6", or "8" seconds
        resolution: "720p", "1080p", or "4k"
        model: Video model name (default: config.DEFAULT_VIDEO_MODEL)
        provider: Provider override

    Returns:
        dict with 'status', 'task_id', and 'result_url'
    """
    model = model or config.DEFAULT_VIDEO_MODEL
    provider_module, provider_name = get_video_provider(model, provider)

    print_status(f"Generating video via {provider_name} ({model})...")
    if image_urls:
        print_status(f"Using {len(image_urls)} image URL(s) (start + anchors)")

    # Submit video task
    operation_id = provider_module.submit_video(
        prompt, 
        image_urls=image_urls,
        model=model, duration=duration, aspect_ratio=aspect_ratio,
        resolution=resolution,
    )
    print_status(f"Task created: {operation_id}", "OK")

    # Poll for result
    return provider_module.poll_video(operation_id, max_wait=600, poll_interval=10)


def generate_for_record(record, model=None, provider=None,
                        aspect_ratio="9:16", duration="8", resolution="720p",
                        num_variations=1):
    """
    Generate video variation(s) for a single Airtable record.

    Uses the record's 'Video Prompt' and 'Generated Image 1' (as start frame).
    Also attaches 'Reference Images' from Airtable as anchors for consistency.

    Args:
        record: Airtable record dict (with 'id' and 'fields')
        model: Video model name
        provider: Provider override
        aspect_ratio: "9:16" or "16:9"
        duration: Video duration in seconds
        resolution: "720p", "1080p", or "4k"
        num_variations: 1 or 2

    Returns:
        list of result dicts, or None if skipped
    """
    model = model or config.DEFAULT_VIDEO_MODEL
    provider_module, provider_name = get_video_provider(model, provider)

    record_id = record["id"]
    fields = record.get("fields", {})
    ad_name = fields.get("Ad Name", "untitled")
    prompt = fields.get("Video Prompt", "")

    if not prompt:
        print_status(f"Skipping '{ad_name}' - no Video Prompt set", "!!")
        return None

    # Combined image list: [Start Frame, Anchor 1, Anchor 2, ...]
    image_urls = []
    
    gen_images = fields.get("Generated Image 1", [])
    if gen_images:
        image_urls.append(gen_images[0].get("url"))

    ref_attachments = fields.get("Reference Images", [])
    image_urls.extend([at.get("url") for at in ref_attachments if at.get("url")])

    num_variations = max(1, min(2, num_variations))
    var_range = range(1, num_variations + 1)

    print(f"\n--- Generating {num_variations} video variation(s) for: {ad_name} ({provider_name}) ---")
    print_status(f"Aspect ratio: {aspect_ratio}")
    print_status(f"Duration: {duration}s")
    print_status(f"Resolution: {resolution}")
    print_status(f"Prompt: {prompt[:100]}{'...' if len(prompt) > 100 else ''}")
    if image_urls:
        print_status(f"Source image: {image_urls[0][:60]}...")

    results = []

    # Submit all variations
    operation_ids = []
    for var_num in var_range:
        print_status(f"Submitting variation {var_num}/{num_variations}...")
        op_id = provider_module.submit_video(
            prompt, image_urls=image_urls,
            model=model, duration=duration,
            aspect_ratio=aspect_ratio, resolution=resolution,
        )
        operation_ids.append(op_id)
        print_status(f"Task {op_id}", "OK")
        if var_num < num_variations:
            time.sleep(2)

    # Poll all
    print_status("Polling for results...")
    results_map = provider_module.poll_tasks_parallel(
        operation_ids, max_wait=600, poll_interval=10
    )
    for op_id in operation_ids:
        result = results_map[op_id]
        if result.get("status") == "error":
            raise Exception(f"Video generation failed: {result.get('error')}")
        results.append(result)

    # Update Airtable
    update_fields = {
        "Video Status": "Generated",
        "Video Model": _MODEL_DISPLAY_NAMES.get(model, model),
    }
    for var_num, result in enumerate(results, 1):
        update_fields[f"Generated Video {var_num}"] = [{"url": result["result_url"]}]
        if result.get("masked_url"):
            update_fields[f"Masked Video {var_num}"] = [{"url": result["masked_url"]}]

    update_record(record_id, update_fields)
    print_status(f"Airtable updated for '{ad_name}' ({num_variations} video variation(s))", "OK")

    return results


def _resolve_record_model(record, fallback_model=None, fallback_provider=None):
    """
    Resolve the model and provider for a single record from its Airtable fields.

    Reads the record's 'Video Model' field (Airtable display name like "Veo 3.1")
    and maps it to the internal model name.
    """
    fields = record.get("fields", {})
    airtable_model = fields.get("Video Model")

    if airtable_model:
        internal = _AIRTABLE_TO_INTERNAL.get(airtable_model)
        if internal:
            provider_module, provider_name = get_video_provider(internal, fallback_provider)
            return internal, provider_module, provider_name

    model = fallback_model or config.DEFAULT_VIDEO_MODEL
    provider_module, provider_name = get_video_provider(model, fallback_provider)
    return model, provider_module, provider_name


def generate_batch(records, model=None, provider=None,
                   aspect_ratio="9:16", duration="8", resolution="720p",
                   num_variations=1):
    """
    Generate videos for multiple Airtable records.

    Respects each record's 'Video Model' field from Airtable.
    Uses 'Generated Image 1' as the source frame for each video.
    Attaches 'Reference Images' from Airtable for product consistency.

    Args:
        records: List of Airtable record dicts
        model: Fallback video model name (default: config.DEFAULT_VIDEO_MODEL)
        provider: Provider override
        aspect_ratio: Override aspect ratio for all records
        duration: Video duration in seconds
        resolution: "720p", "1080p", or "4k"
        num_variations: Videos per record, 1 or 2 (default: 1)

    Returns:
        list of results (None for skipped/failed records)
    """
    actionable = [r for r in records if r.get("fields", {}).get("Video Prompt")]
    count = len(actionable)

    if count == 0:
        print_status("No records with Video Prompt found - nothing to generate", "!!")
        return []

    # --- Resolve per-record models and build cost summary ---
    record_models = {}
    cost_groups = {}
    for record in actionable:
        internal, pmod, pname = _resolve_record_model(record, model, provider)
        record_models[record["id"]] = (internal, pmod, pname)
        key = (internal, pname)
        cost_groups[key] = cost_groups.get(key, 0) + 1

    num_variations = max(1, min(2, num_variations))
    var_range = range(1, num_variations + 1)
    videos_total = count * num_variations
    total_cost = 0.0

    print(f"\n{'=' * 50}")
    print(f"  Video Generation Batch")
    print(f"{'=' * 50}")
    print(f"  Records: {count}")
    print(f"  Videos per record: {num_variations} (variations)")
    print(f"  Total videos: {videos_total}")
    print(f"  Aspect ratio: {aspect_ratio}")
    print(f"  Duration: {duration}s")
    print(f"  Resolution: {resolution}")
    for (m, pname), rec_count in cost_groups.items():
        unit = config.get_cost(m, pname)
        group_cost = rec_count * num_variations * unit
        total_cost += group_cost
        display = _MODEL_DISPLAY_NAMES.get(m, m)
        print(f"  {display} via {pname}: {rec_count} record(s) x {num_variations} = {rec_count * num_variations} videos @ ${unit:.2f} = ${group_cost:.2f}")
    print(f"  Total estimated cost: ${total_cost:.2f}")
    print(f"{'=' * 50}\n")

    # --- Phase 1: Submit all video tasks ---
    print(f"\n--- Phase 1: Submitting {videos_total} video tasks ---")

    # submissions: list of (record, var_num, operation_id, model, provider_module, provider_name)
    submissions = []

    for record in actionable:
        fields = record.get("fields", {})
        ad_name = fields.get("Ad Name", "untitled")

        # Combined image list
        image_urls = []
        gen_images = fields.get("Generated Image 1", [])
        if gen_images:
            image_urls.append(gen_images[0].get("url"))

        ref_attachments = fields.get("Reference Images", [])
        image_urls.extend([at.get("url") for at in ref_attachments if at.get("url")])

        prompt = fields.get("Video Prompt", "")
        rec_model, rec_pmod, rec_pname = record_models[record["id"]]
        display_model = _MODEL_DISPLAY_NAMES.get(rec_model, rec_model)

        for var_num in var_range:
            print_status(f"Submitting: {ad_name} (variation {var_num}) [{display_model} via {rec_pname}]")
            try:
                op_id = rec_pmod.submit_video(
                    prompt, image_urls=image_urls,
                    model=rec_model, duration=duration,
                    aspect_ratio=aspect_ratio, resolution=resolution,
                )
                submissions.append((record, var_num, op_id, rec_model, rec_pmod, rec_pname))
                print_status(f"Task {op_id}", "OK")
            except Exception as e:
                print_status(f"Failed: {e}", "XX")
                submissions.append((record, var_num, None, rec_model, rec_pmod, rec_pname))
            time.sleep(2)

    # --- Phase 2: Poll all tasks (grouped by provider) ---
    results_map = {}

    tasks_by_provider = {}
    for record, var_num, op_id, rec_model, rec_pmod, rec_pname in submissions:
        if op_id is not None:
            tasks_by_provider.setdefault(rec_pmod, []).append(op_id)

    for pmod, op_ids in tasks_by_provider.items():
        print(f"\n--- Phase 2: Polling {len(op_ids)} video tasks ---")
        polled = pmod.poll_tasks_parallel(op_ids, max_wait=600, poll_interval=10)
        results_map.update(polled)

    # --- Phase 3: Update Airtable per record ---
    print(f"\n--- Phase 3: Updating Airtable ---")
    record_tasks = {}
    for record, var_num, op_id, rec_model, rec_pmod, rec_pname in submissions:
        rid = record["id"]
        if rid not in record_tasks:
            record_tasks[rid] = []
        record_tasks[rid].append((var_num, op_id))

    record_map = {r["id"]: r for r in actionable}
    results = []
    succeeded = 0
    videos_generated = 0
    actual_cost = 0.0

    for rid, tasks in record_tasks.items():
        record = record_map[rid]
        ad_name = record.get("fields", {}).get("Ad Name", "untitled")
        rec_model, _, rec_pname = record_models[rid]
        update_fields = {}
        record_ok = True

        for var_num, op_id in tasks:
            if op_id is None:
                record_ok = False
                continue
            result = results_map.get(op_id, {})
            if result.get("status") == "error":
                print_status(f"'{ad_name}' variation {var_num} failed: {result.get('error')}", "XX")
                record_ok = False
            else:
                update_fields[f"Generated Video {var_num}"] = [{"url": result["result_url"]}]
                if result.get("masked_url"):
                    update_fields[f"Masked Video {var_num}"] = [{"url": result["masked_url"]}]
                videos_generated += 1
                actual_cost += config.get_cost(rec_model, rec_pname)

        if update_fields:
            update_fields["Video Status"] = "Generated"
            update_fields["Video Model"] = _MODEL_DISPLAY_NAMES.get(rec_model, rec_model)
            update_record(rid, update_fields)
            print_status(f"Airtable updated for '{ad_name}'", "OK")

        if record_ok:
            succeeded += 1
        
        # Ensure we return a useful record object for the caller
        summary = {
            "ad_name": ad_name,
            "status": "success" if record_ok else "error",
            "updates": update_fields
        }
        results.append(summary)

    print(f"\n{'=' * 50}")
    print(f"  Batch complete: {succeeded}/{count} records ({videos_generated} videos)")
    print(f"  Actual cost: ${actual_cost:.2f}")
    print(f"{'=' * 50}\n")

    return results
