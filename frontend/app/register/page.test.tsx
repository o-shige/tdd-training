/**登録フォームページのテスト
 * 
 * t_wada形式のTDDで進めます。
 * 1. Red: 失敗するテストを書く
 * 2. Green: 最小限の実装でテストを通す
 * 3. Refactor: コードをきれいにする
 */

import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import RegisterPage from './page'

describe('RegisterPage', () => {
  it('登録フォームページが表示される', () => {
    render(<RegisterPage />)
    
    // ページタイトルが表示されることを確認
    expect(screen.getByText(/ユーザー登録/i)).toBeInTheDocument()
  })

  it('メールアドレス入力フィールドが表示される', () => {
    render(<RegisterPage />)
    
    // メールアドレス入力フィールドが存在することを確認
    expect(screen.getByLabelText(/メールアドレス/i)).toBeInTheDocument()
  })

  it('パスワード入力フィールドが表示される', () => {
    render(<RegisterPage />)
    
    // パスワード入力フィールドが存在することを確認
    expect(screen.getByLabelText(/パスワード/i)).toBeInTheDocument()
  })

  it('メールアドレスが空の場合、エラーメッセージが表示される', async () => {
    const user = userEvent.setup()
    render(<RegisterPage />)
    
    // パスワードのみ入力
    const passwordInput = screen.getByLabelText(/パスワード/i)
    await user.type(passwordInput, 'password123')
    
    // フォーム送信
    const submitButton = screen.getByRole('button', { name: /登録/i })
    await user.click(submitButton)
    
    // エラーメッセージが表示されることを確認
    expect(screen.getByText(/メールアドレスは必須です/i)).toBeInTheDocument()
  })
})

