"use client";

import { type ReactNode, useRef, useState } from "react";
import { Button, type ButtonProps } from "@/components/core/button";

type ClipBordButtonProps = Omit<ButtonProps, "children" | "onClick"> & {
  text: string;
  children: (cliped: boolean) => ReactNode;
};

export const ClipBordButton = ({
  text,
  children,
  ...rest
}: ClipBordButtonProps) => {
  const [cliped, setCliped] = useState(false);
  const timeRef = useRef<NodeJS.Timeout | null>(null);

  const handleClick = async () => {
    navigator.clipboard
      .writeText(text)
      .then(() => {
        setCliped(true);
        if (timeRef.current) {
          clearTimeout(timeRef.current);
        }
        timeRef.current = setTimeout(() => {
          setCliped(false);
        }, 1000);
      })
      .catch(() => {
        setCliped(false);
      });
  };

  return (
    <Button type="button" onClick={handleClick} {...rest}>
      {children(cliped)}
    </Button>
  );
};
