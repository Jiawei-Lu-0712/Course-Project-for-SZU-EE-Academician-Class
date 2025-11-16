#include "model_data.h"
#include "tensorflow/lite/micro/all_ops_resolver.h"
#include "tensorflow/lite/micro/micro_interpreter.h"
#include "tensorflow/lite/schema/schema_generated.h"

constexpr int kTensorArenaSize = 150 * 1024;
static uint8_t tensor_arena[kTensorArenaSize];

void setup() {
  // 初始化串口
  Serial.begin(115200);
  // 初始化传感器、I2S
  MPU6886.Init();
  initI2S();
  // 加载模型
  const tflite::Model* model = tflite::GetModel(g_model_data);
  static tflite::AllOpsResolver resolver;
  static tflite::MicroInterpreter interpreter(
      model, resolver, tensor_arena, kTensorArenaSize, nullptr);
  interpreter.AllocateTensors();
}

void loop() {
  // 1. 采集手势、语音、体感数据
  readIMU(imu_buf);       // e.g. 6 floats
  readAudio(audio_buf);   // e.g. 512 samples
  readMotion(motion_buf); // 自定义

  // 2. 填充输入张量
  uint8_t* input = interpreter.input(0)->data.uint8;
  packInputs(input, imu_buf, audio_buf, motion_buf);

  // 3. 推理
  interpreter.Invoke();
  // 4. 读取输出
  uint8_t* output = interpreter.output(0)->data.uint8;
  // 5. 解码综合意图（argmax 或者多标签阈值）
  auto intent = decodeIntent(output);
  Serial.printf("Detected intent: %d\n", intent);

  delay(50);
}
