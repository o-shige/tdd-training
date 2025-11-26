/**バリデーション関数
 * 
 * 登録フォームのバリデーションロジックを純粋関数として実装します。
 * PBTテストでテストしやすくするため、コンポーネントから分離します。
 */

export interface ValidationResult {
  isValid: boolean
  emailError?: string
  passwordError?: string
}

export function validateRegistrationForm(email: string, password: string): ValidationResult {
  const result: ValidationResult = { isValid: true }

  // メールアドレスのバリデーション
  if (!email || email.trim() === '') {
    result.isValid = false
    result.emailError = 'メールアドレスは必須です'
  }

  // パスワードのバリデーション
  if (!password || password.length < 8) {
    result.isValid = false
    result.passwordError = 'パスワードは8文字以上で入力してください'
  }

  return result
}

