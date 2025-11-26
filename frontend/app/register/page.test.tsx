/**登録フォームページのテスト
 * 
 * t_wada形式のTDDで進めます。
 * 1. Red: 失敗するテストを書く
 * 2. Green: 最小限の実装でテストを通す
 * 3. Refactor: コードをきれいにする
 */

import { render, screen } from '@testing-library/react'
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
})

