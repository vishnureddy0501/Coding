"use client";

import Image from "next/image";
import { Pin, usePinsStore } from "@/store/pins.store";

export default function PinCard({ pin }: { pin: Pin }) {
  const openPin = usePinsStore((s) => s.openPin);

  return (
    <button
      onClick={() => openPin(pin)}
      className="relative rounded-xl overflow-hidden bg-neutral-200 hover:opacity-90 transition"
      style={{ height: pin.height }}
    >
      <Image
        src={pin.image}
        alt={pin.title}
        fill
        sizes="(max-width: 768px) 50vw, 25vw"
        className="object-cover"
        priority={false}
      />
    </button>
  );
}
