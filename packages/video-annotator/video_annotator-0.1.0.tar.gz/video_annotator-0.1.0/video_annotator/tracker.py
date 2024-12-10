# video_annotator/tracker.py

import supervision as sv

class AdvancedVideoTracker:
    def __init__(self, model, ellipse_colors, label_colors, label_text_color, triangle_color, 
                 triangle_base=25, triangle_height=21, padding_px=10):
        self.model = model
        self.padding_px = padding_px
        
        # Initialize annotators
        self.ellipse_annotator = sv.EllipseAnnotator(
            color=sv.ColorPalette.from_hex(ellipse_colors),
            thickness=2
        )
        self.label_annotator = sv.LabelAnnotator(
            color=sv.ColorPalette.from_hex(label_colors),
            text_color=sv.Color.from_hex(label_text_color),
            text_position=sv.Position.BOTTOM_CENTER
        )
        self.triangle_annotator = sv.TriangleAnnotator(
            color=sv.Color.from_hex(triangle_color),
            base=triangle_base,
            height=triangle_height,
            outline_thickness=1
        )
        
        # Initialize tracker
        self.tracker = sv.ByteTrack()

    def annotate_frame(self, frame, ball_id, confidence_threshold=0.3, nms_threshold=0.5):
        # Run inference
        result = self.model.infer(frame, confidence=confidence_threshold)[0]
        detections = sv.Detections.from_inference(result)

        # Process ball detections
        ball_detections = detections[detections.class_id == ball_id]
        ball_detections.xyxy = sv.pad_boxes(xyxy=ball_detections.xyxy, px=self.padding_px)

        # Process and track other detections
        all_detections = detections[detections.class_id != ball_id]
        all_detections = all_detections.with_nms(threshold=nms_threshold, class_agnostic=True)
        all_detections.class_id -= 1
        all_detections = self.tracker.update_with_detections(detections=all_detections)

        # Generate labels for tracked objects
        labels = [
            f"#{tracker_id}"
            for tracker_id
            in all_detections.tracker_id
        ]

        # Annotate frame
        annotated_frame = frame.copy()
        annotated_frame = self.ellipse_annotator.annotate(
            scene=annotated_frame,
            detections=all_detections
        )
        annotated_frame = self.label_annotator.annotate(
            scene=annotated_frame,
            detections=all_detections,
            labels=labels
        )
        annotated_frame = self.triangle_annotator.annotate(
            scene=annotated_frame,
            detections=ball_detections
        )
        return annotated_frame
