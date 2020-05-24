BASE_DIR = "/faceEditor/"
TEMP_DIR = "temp/"
THUMBNAIL_SIZE = 256, 256

# MODEL
MODEL = "MODELS/generator_13.h5"
MODEL_SIZE_SGM = 256, 256
MODEL_SIZE_ORG = 256, 256

# MODEL CORAL
#MODEL_CORAL = "MODELS/converted_model_quant_256tf2_edgetpu.tflite"
MODEL_CORAL = "MODELS/converted_model_quant_256tf2.tflite"
#MODEL_CORAL = "MODELS/mobilenet_v1_1.0_224_quant_edgetpu.tflite"
MODEL_CORAL_SIZE_SGM = 256, 256
MODEL_CORAL_SIZE_ORG = 256, 256

SAVE_DATA = True
