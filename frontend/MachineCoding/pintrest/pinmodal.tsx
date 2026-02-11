"use client";

import { useEffect } from "react";
import Image from "next/image";
import { usePinsStore } from "@/store/pins.store";

export default function PinModal() {
  const { selectedPin, closePin } = usePinsStore();

  useEffect(() => {
    if (!selectedPin) return;

    const esc = (e: KeyboardEvent) => e.key === "Escape" && closePin();
    document.addEventListener("keydown", esc);
    document.body.style.overflow = "hidden";

    return () => {
      document.removeEventListener("keydown", esc);
      document.body.style.overflow = "";
    };
  }, [selectedPin, closePin]);

  if (!selectedPin) return null;

  return (
    <div
      onClick={closePin}
      className="fixed inset-0 z-50 bg-black/60 flex items-center justify-center"
    >
      <div
        onClick={(e) => e.stopPropagation()}
        className="relative bg-white rounded-2xl max-w-3xl w-full h-[80vh] overflow-hidden"
      >
        <Image
          src={selectedPin.image}
          alt={selectedPin.title}
          fill
          className="object-contain"
          priority
        />
      </div>
    </div>
  );
}
