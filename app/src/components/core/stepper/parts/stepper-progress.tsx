export type StepperProgressProps = {
  current: number;
  progress: number;
};

export const StepperProgress = ({
  current,
  progress,
}: StepperProgressProps) => {
  const radius = (60 - 4) / 2;
  const circumference = 2 * Math.PI * radius;
  const offset = circumference * (1 - current / progress);

  return (
    <div
      className="relative flex items-center justify-center"
      style={{ width: 60, height: 60 }}
    >
      {/* biome-ignore lint/a11y/noSvgWithoutTitle: <explanation> */}
      <svg width={60} height={60} style={{ transform: "rotate(-90deg)" }}>
        <circle
          cx={60 / 2}
          cy={60 / 2}
          r={radius}
          strokeWidth={4}
          fill="none"
          className="stroke-gray-300"
        />
        <circle
          cx={60 / 2}
          cy={60 / 2}
          r={radius}
          strokeWidth={4}
          fill="none"
          strokeDasharray={circumference}
          strokeDashoffset={offset}
          strokeLinecap="round"
          className="stroke-blue-800"
        />
      </svg>
      <span className="absolute inset-0 flex items-center justify-center text-lg font-bold">
        {`${current}/${progress}`}
      </span>
    </div>
  );
};
