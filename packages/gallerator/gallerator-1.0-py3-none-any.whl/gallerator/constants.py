generated_dir_basename = 'generated-images'

digest = 'sha1'

thumbnail_target_pixels = 350*350

# If we just let vcsi create a single image, it will do so towards the
# middle of the video. Testing shows that the first image in the contact
# sheet, about 12% into the video, is better. Find the time 12% in:
video_thumbnail_time_fraction = 0.12