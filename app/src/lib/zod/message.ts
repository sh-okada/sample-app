export const message = {
  required: (label: string) => `${label}は必須項目です`,
  isPastOrToday: (label: string) => `${label}は未来の日付を選択できません`,
  min: (label: string, min: number) =>
    `${label}は${min}文字以上で入力してください`,
  max: (label: string, max: number) =>
    `${label}は${max}文字以下で入力してください`,
} as const;
