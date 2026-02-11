"use client";

import { useEffect } from "react";
import MasonryGrid from "@/components/MasonryGrid";
import PinModal from "@/components/PinModal";
import { generatePins } from "@/lib/mockPins";
import { usePinsStore } from "@/store/pins.store";
import { useInfiniteScroll } from "@/hooks/useInfiniteScroll";

export default function HomePage() {
  const addPins = usePinsStore((s) => s.addPins);

  useEffect(() => {
    addPins(generatePins(20));
  }, [addPins]);

  const loadMoreRef = useInfiniteScroll(() => {
    addPins(generatePins(10));
  });

  return (
    <>
      <MasonryGrid />
      <div ref={loadMoreRef} className="h-10" />
      <PinModal />
    </>
  );
}
