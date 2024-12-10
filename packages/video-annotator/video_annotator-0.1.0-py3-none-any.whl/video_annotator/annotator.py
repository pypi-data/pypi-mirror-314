# video_annotator/annotator.py

import supervision as sv

class VideoAnnotator:
    def __init__(self, model, box_colors, label_colors, label_text_color, box_thickness=2):
        self.model = model
        self.box_annotator = sv.BoxAnnotator(
            color=sv.ColorPalette.from_hex(box_colors),
            thickness=box_thickness
        )
        self.label_annotator = sv.LabelAnnotator(
            color=sv.ColorPalette.from_hex(label_colors),
            text_color=sv.Color.from_hex(label_text_color)
        )

    def annotate_frame(self, frame, confidence_threshold):
        # Run inference on the frame
        result = self.model.infer(frame, confidence=confidence_threshold)[0]
        detections = sv.Detections.from_inference(result)

        # Generate labels for the detections
        labels = [
            f"{class_name} {confidence:.2f}"
            for class_name, confidence
            in zip(detections['class_name'], detections.confidence)
        ]

        # Annotate frame with boxes and labels
        annotated_frame = frame.copy()
        annotated_frame = self.box_annotator.annotate(
            scene=annotated_frame,
            detections=detections
        )
        annotated_frame = self.label_annotator.annotate(
            scene=annotated_frame,
            detections=detections,
            labels=labels
        )
        return annotated_frame
