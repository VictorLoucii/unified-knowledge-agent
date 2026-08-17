// frontend/src/hooks/useAudioVisualizer.ts
import { useState, useEffect, useRef } from 'react';

export function useAudioVisualizer(isListening: boolean, barCount: number = 20) {
  // Default to a small minimal height when idle
  const [audioData, setAudioData] = useState<number[]>(new Array(barCount).fill(15));
  const audioContextRef = useRef<AudioContext | null>(null);
  const analyserRef = useRef<AnalyserNode | null>(null);
  const sourceRef = useRef<MediaStreamAudioSourceNode | null>(null);
  const animationRef = useRef<number | null>(null);
  const streamRef = useRef<MediaStream | null>(null);

  useEffect(() => {
    // If not listening, cleanly reset everything
    if (!isListening) {
      if (animationRef.current) cancelAnimationFrame(animationRef.current);
      if (streamRef.current) streamRef.current.getTracks().forEach(t => t.stop());
      if (audioContextRef.current && audioContextRef.current.state !== 'closed') {
        audioContextRef.current.close().catch(() => {});
      }
      setAudioData(new Array(barCount).fill(15));
      return;
    }

    let isMounted = true;

    const startAudioProcessing = async () => {
      try {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        if (!isMounted) return;
        
        streamRef.current = stream;
        
        // Initialize Web Audio Context
        const audioCtx = new (window.AudioContext || (window as any).webkitAudioContext)();
        audioContextRef.current = audioCtx;
        
        const analyser = audioCtx.createAnalyser();
        // Lower fftSize yields a smoother, less jagged response for speech
        analyser.fftSize = 256; 
        analyserRef.current = analyser;
        
        const source = audioCtx.createMediaStreamSource(stream);
        source.connect(analyser);
        sourceRef.current = source;
        
        const bufferLength = analyser.frequencyBinCount;
        const dataArray = new Uint8Array(bufferLength);
        
        const updateData = () => {
          if (!isMounted || !analyserRef.current) return;
          
          analyserRef.current.getByteFrequencyData(dataArray);
          
          const newAudioData = [];
          const step = Math.floor((bufferLength * 0.75) / barCount); // Cut off highest frequencies for speech
          
          for (let i = 0; i < barCount; i++) {
            let sum = 0;
            for (let j = 0; j < step; j++) {
              sum += dataArray[i * step + j];
            }
            const avg = sum / step;
            // Map the average byte value (0-255) to a CSS percentage height (15% to 100%)
            const height = Math.max(15, Math.min(100, (avg / 255) * 100 * 1.5)); 
            newAudioData.push(height);
          }
          
          setAudioData(newAudioData);
          animationRef.current = requestAnimationFrame(updateData);
        };
        
        updateData();
      } catch (err) {
        console.error("Error accessing microphone for visualizer:", err);
      }
    };

    startAudioProcessing();

    return () => {
      isMounted = false;
      if (animationRef.current) cancelAnimationFrame(animationRef.current);
      if (streamRef.current) streamRef.current.getTracks().forEach(t => t.stop());
      if (audioContextRef.current && audioContextRef.current.state !== 'closed') {
        audioContextRef.current.close().catch(() => {});
      }
    };
  }, [isListening, barCount]);

  return audioData;
}
