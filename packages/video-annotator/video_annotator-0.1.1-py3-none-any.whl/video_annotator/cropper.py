# video_annotator/cropper.py

import supervision as sv
from tqdm import tqdm

class CropCollector:
    def __init__(self, model, stride=1, confidence_threshold=0.3, nms_threshold=0.5):
        self.model = model
        self.stride = stride
        self.confidence_threshold = confidence_threshold
        self.nms_threshold = nms_threshold

    def collect_crops(self, video_path, class_id):
        frame_generator = sv.get_video_frames_generator(
            source_path=video_path, stride=self.stride)
        
        crops = []
        for frame in tqdm(frame_generator, desc="Collecting crops"):
            result = self.model.infer(frame, confidence=self.confidence_threshold)[0]
            detections = sv.Detections.from_inference(result)

            detections = detections.with_nms(threshold=self.nms_threshold, class_agnostic=True)
            filtered_detections = detections[detections.class_id == class_id]

            frame_crops = [sv.crop_image(frame, xyxy) for xyxy in filtered_detections.xyxy]
            crops.extend(frame_crops)
        
        return crops
