import { onMount } from "svelte";
import { Recorder } from "./audio/recorder";

const BUFFER_SIZE = 4800;

export default function useAudioRecorder({onAudioRecorded}) {
    let audioRecorder;
    let buffer = new Uint8Array();

    const appendToBuffer = (newData) => {
        const newBuffer = new Uint8Array(buffer.length + newData.length);
        newBuffer.set(buffer);
        newBuffer.set(newData, buffer.length);
        buffer = newBuffer;
    };

    const handleAudioData = (data) => {
        const uint8Array = new Uint8Array(data);
        appendToBuffer(uint8Array);

        if (buffer.length >= BUFFER_SIZE) {
            const toSend = new Uint8Array(buffer.slice(0, BUFFER_SIZE));
            buffer = new Uint8Array(buffer.slice(BUFFER_SIZE));

            const regularArray = String.fromCharCode(...toSend);
            const base64 = btoa(regularArray);

            onAudioRecorded(base64);
        }
    };

    const start = async () => {
        if (!audioRecorder) {
            audioRecorder = new Recorder(handleAudioData);
        }
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        audioRecorder.start(stream);
    };

    const stop = async () => {
        await audioRecorder?.stop();
    };

    onMount(() => {
        // Cleanup logic if needed
        return () => {
            stop();
        };
    });

    return { start, stop };
}
