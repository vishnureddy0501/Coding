import { Pin } from "@/store/pins.store";

export function generatePins(count = 10): Pin[] {
  return Array.from({ length: count }).map((_, i) => ({
    id: crypto.randomUUID(),
    image: `https://picsum.photos/600/8${i}`,
    title: "Pinterest Pin",
    height: 300 + Math.floor(Math.random() * 300),
  }));
}
