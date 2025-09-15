// web/src/components/ui/Button.tsx
import * as React from "react";
import { cva, type VariantProps } from "class-variance-authority";
import { cn } from "../../lib/utils";
import { motion, type HTMLMotionProps } from "framer-motion";

const button = cva(
  "inline-flex items-center gap-2 rounded-xl font-medium transition focus:outline-none focus-visible:ring-2 ring-indigo-400/40 disabled:opacity-60 disabled:cursor-not-allowed",
  {
    variants: {
      intent: {
        primary: "bg-indigo-500 hover:bg-indigo-400 text-white",
        ghost: "bg-white/5 hover:bg-white/10 border border-white/10 text-white/90",
        subtle: "bg-white/7 hover:bg-white/12 text-white/90"
      },
      size: {
        sm: "px-3 py-1.5 text-sm",
        md: "px-4 py-2",
        lg: "px-5 py-2.5 text-base"
      }
    },
    defaultVariants: { intent: "primary", size: "md" }
  }
);

// ✅ Use Framer Motion’s HTMLMotionProps<'button'> as the base props
type ButtonBaseProps = Omit<HTMLMotionProps<"button">, "ref">;
type ButtonProps = ButtonBaseProps & VariantProps<typeof button> & { className?: string };

export const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(function Button(
  { className, intent, size, whileHover = { scale: 1.02 }, whileTap = { scale: 0.97 }, ...rest },
  ref
) {
  return (
    <motion.button
      ref={ref}
      whileHover={whileHover}
      whileTap={whileTap}
      className={cn(button({ intent, size }), className)}
      {...rest}
    />
  );
});
