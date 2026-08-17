import 'regenerator-runtime/runtime';
import { useCallback, useEffect } from 'react';
import SpeechRecognition, { useSpeechRecognition } from 'react-speech-recognition';

export function useVoiceRecording() {
  const {
    transcript,
    listening,
    resetTranscript,
    browserSupportsSpeechRecognition,
    isMicrophoneAvailable,
  } = useSpeechRecognition();

  useEffect(() => {
    console.log("[VoiceDebug] listening:", listening, " | transcript:", transcript, " | micAvailable:", isMicrophoneAvailable);
  }, [listening, transcript, isMicrophoneAvailable]);

  const startRecording = useCallback(() => {
    resetTranscript();
    SpeechRecognition.startListening({ continuous: true, language: 'en-US', interimResults: true });
  }, [resetTranscript]);

  const stopRecording = useCallback(() => {
    SpeechRecognition.stopListening();
  }, []);

  return {
    transcript,
    isListening: listening,
    startRecording,
    stopRecording,
    resetTranscript,
    browserSupportsSpeechRecognition
  };
}
