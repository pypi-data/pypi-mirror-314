import { Player } from "./audio/player";

const SAMPLE_RATE = 24000;

let audioPlayer: Player | null = null;

export function reset() {
    audioPlayer = new Player();
    audioPlayer.init(SAMPLE_RATE);
}

export function play(base64Audio: string) {
    const binary = atob(base64Audio);
    const bytes = Uint8Array.from(binary, c => c.charCodeAt(0));
    const pcmData = new Int16Array(bytes.buffer);

    audioPlayer?.play(pcmData);
}

export function stop() {
    audioPlayer?.stop();
}