import { Haptics } from "@capacitor/haptics"

export async function HapticFeedback() {
  await Haptics.vibrate();
}