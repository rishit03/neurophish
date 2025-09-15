export function cn(...cls: (string | undefined | false)[]) {
  return cls.filter(Boolean).join(" ");
}