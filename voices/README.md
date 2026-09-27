# Voices

Put Piper voice models (`*.onnx` + matching `*.onnx.json`) in this folder. The app lists every model it finds here.

```sh
base=https://huggingface.co/rhasspy/piper-voices/resolve/main/ru/ru_RU
for v in denis irina; do
  curl -L -o ru_RU-$v-medium.onnx      $base/$v/medium/ru_RU-$v-medium.onnx
  curl -L -o ru_RU-$v-medium.onnx.json $base/$v/medium/ru_RU-$v-medium.onnx.json
done
```

The voice models are not part of this repository and have their own licenses (see the model cards on
[Hugging Face](https://huggingface.co/rhasspy/piper-voices/tree/main/ru/ru_RU)).
