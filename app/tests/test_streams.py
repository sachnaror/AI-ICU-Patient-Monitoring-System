from app.video_processing.opencv_utils import synthetic_icu_frame


def test_synthetic_frame_shape_and_context():
    frame, context = synthetic_icu_frame(1)
    assert frame.shape == (540, 960, 3)
    assert "spo2" in context
    assert "patient_box" in context
