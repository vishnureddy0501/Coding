import { create } from "zustand";

export type Pin = {
  id: string;
  image: string;
  title: string;
  height: number;
};

type PinsState = {
  pins: Pin[];
  selectedPin: Pin | null;
  addPins: (newPins: Pin[]) => void;
  openPin: (pin: Pin) => void;
  closePin: () => void;
};

export const usePinsStore = create<PinsState>((set) => ({
  pins: [],
  selectedPin: null,

  addPins: (newPins) =>
    set((state) => ({
      pins: [...state.pins, ...newPins],
    })),

  openPin: (pin) => set({ selectedPin: pin }),
  closePin: () => set({ selectedPin: null }),
}));
