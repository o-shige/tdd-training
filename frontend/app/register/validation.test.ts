/**バリデーション関数のプロパティベースドテスト（PBT）
 * 
 * fast-checkを使用して、バリデーション関数のプロパティをテストします。
 */

import fc from 'fast-check'
import { validateRegistrationForm } from './validation'

describe('validateRegistrationForm Property-Based Tests', () => {
  it('有効なメールアドレスと8文字以上のパスワードなら常にバリデーションが成功する', () => {
    fc.assert(
      fc.property(
        fc.emailAddress(), // 有効なメールアドレスを生成
        fc.string({ minLength: 8, maxLength: 100 }), // 8文字以上のパスワード
        (email, password) => {
          const result = validateRegistrationForm(email, password)
          expect(result.isValid).toBe(true)
          expect(result.emailError).toBeUndefined()
          expect(result.passwordError).toBeUndefined()
        }
      ),
      { numRuns: 100 } // 100回のランダムテストを実行
    )
  })

  it('7文字以下のパスワードなら常にバリデーションが失敗する', () => {
    fc.assert(
      fc.property(
        fc.emailAddress(),
        fc.string({ minLength: 1, maxLength: 7 }), // 7文字以下のパスワード
        (email, password) => {
          const result = validateRegistrationForm(email, password)
          expect(result.isValid).toBe(false)
          expect(result.passwordError).toBe('パスワードは8文字以上で入力してください')
        }
      ),
      { numRuns: 100 }
    )
  })

  it('空のメールアドレスなら常にバリデーションが失敗する', () => {
    fc.assert(
      fc.property(
        fc.constant(''), // 空文字列
        fc.string({ minLength: 8, maxLength: 100 }),
        (email, password) => {
          const result = validateRegistrationForm(email, password)
          expect(result.isValid).toBe(false)
          expect(result.emailError).toBe('メールアドレスは必須です')
        }
      ),
      { numRuns: 10 } // 空文字列は1パターンのみなので少なめに
    )
  })

  it('空白のみのメールアドレスなら常にバリデーションが失敗する', () => {
    fc.assert(
      fc.property(
        fc.string({ minLength: 1, maxLength: 10 }).map(s => ' '.repeat(s.length)), // 空白のみの文字列
        fc.string({ minLength: 8, maxLength: 100 }),
        (email, password) => {
          const result = validateRegistrationForm(email, password)
          expect(result.isValid).toBe(false)
          expect(result.emailError).toBe('メールアドレスは必須です')
        }
      ),
      { numRuns: 10 }
    )
  })
})

