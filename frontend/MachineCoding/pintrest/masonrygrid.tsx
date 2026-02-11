"use client";

import { useEffect, useMemo, useState } from "react";
import { usePinsStore } from "@/store/pins.store";
import PinCard from "./PinCard";

const COLUMN_GAP = 16;

export default function MasonryGrid() {
  const pins = usePinsStore((s) => s.pins);
  const [columns, setColumns] = useState(4);

  useEffect(() => {
    const updateColumns = () => {
      if (window.innerWidth < 640) setColumns(2);
      else if (window.innerWidth < 1024) setColumns(3);
      else setColumns(4);
    };

    updateColumns();
    window.addEventListener("resize", updateColumns);
    return () => window.removeEventListener("resize", updateColumns);
  }, []);

  const masonry = useMemo(() => {
    const cols: typeof pins[] = Array.from({ length: columns }, () => []);
    pins.forEach((pin, i) => {
      cols[i % columns].push(pin);
    });
    return cols;
  }, [pins, columns]);

  return (
    <div
      style={{ gap: COLUMN_GAP }}
      className="flex w-full px-4"
    >
      {masonry.map((col, i) => (
        <div key={i} className="flex flex-col gap-4 flex-1">
          {col.map((pin) => (
            <PinCard key={pin.id} pin={pin} />
          ))}
        </div>
      ))}
    </div>
  );
}
