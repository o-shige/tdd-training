/**登録フォームページのテスト
 * 
 * t_wada形式のTDDで進めます。
 * 1. Red: 失敗するテストを書く
 * 2. Green: 最小限の実装でテストを通す
 * 3. Refactor: コードをきれいにする
 */

import { render, screen, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import RegisterPage from './page'

// fetchをモック
global.fetch = jest.fn()

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

  it('パスワードが短い場合、エラーメッセージが表示される', async () => {
    const user = userEvent.setup()
    render(<RegisterPage />)
    
    // メールアドレスと短いパスワードを入力
    const emailInput = screen.getByLabelText(/メールアドレス/i)
    await user.type(emailInput, 'test@example.com')
    const passwordInput = screen.getByLabelText(/パスワード/i)
    await user.type(passwordInput, 'pass123') // 7文字（8文字未満）
    
    // フォーム送信
    const submitButton = screen.getByRole('button', { name: /登録/i })
    await user.click(submitButton)
    
    // エラーメッセージが表示されることを確認（業界標準の8文字以上）
    expect(screen.getByText(/パスワードは8文字以上で入力してください/i)).toBeInTheDocument()
  })

  it('有効なデータで送信するとAPIが呼ばれる', async () => {
    const user = userEvent.setup()
    // API成功レスポンスをモック
    ;(global.fetch as jest.Mock).mockResolvedValueOnce({
      ok: true,
      status: 201,
      json: async () => ({
        id: '123',
        email: 'test@example.com'
      })
    })

    render(<RegisterPage />)
    
    // 有効なデータを入力
    const emailInput = screen.getByLabelText(/メールアドレス/i)
    await user.type(emailInput, 'test@example.com')
    const passwordInput = screen.getByLabelText(/パスワード/i)
    await user.type(passwordInput, 'password123')
    
    // フォーム送信
    const submitButton = screen.getByRole('button', { name: /登録/i })
    await user.click(submitButton)
    
    // APIが呼ばれることを確認
    await waitFor(() => {
      expect(global.fetch).toHaveBeenCalledWith(
        'http://localhost:8000/api/register',
        expect.objectContaining({
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            email: 'test@example.com',
            password: 'password123'
          })
        })
      )
    })
  })

  it('重複メールアドレスで送信するとエラーメッセージが表示される', async () => {
    const user = userEvent.setup()
    // API 409エラーレスポンスをモック
    ;(global.fetch as jest.Mock).mockResolvedValueOnce({
      ok: false,
      status: 409,
      json: async () => ({
        detail: {
          error: 'Email test@example.com is already registered'
        }
      })
    })

    render(<RegisterPage />)
    
    // 有効なデータを入力
    const emailInput = screen.getByLabelText(/メールアドレス/i)
    await user.type(emailInput, 'test@example.com')
    const passwordInput = screen.getByLabelText(/パスワード/i)
    await user.type(passwordInput, 'password123')
    
    // フォーム送信
    const submitButton = screen.getByRole('button', { name: /登録/i })
    await user.click(submitButton)
    
    // エラーメッセージが表示されることを確認
    await waitFor(() => {
      expect(screen.getByText(/このメールアドレスは既に登録されています/i)).toBeInTheDocument()
    })
  })

  it('登録成功時に成功メッセージが表示される', async () => {
    const user = userEvent.setup()
    // API成功レスポンスをモック
    ;(global.fetch as jest.Mock).mockResolvedValueOnce({
      ok: true,
      status: 201,
      json: async () => ({
        id: '123',
        email: 'test@example.com'
      })
    })

    render(<RegisterPage />)
    
    // 有効なデータを入力
    const emailInput = screen.getByLabelText(/メールアドレス/i)
    await user.type(emailInput, 'test@example.com')
    const passwordInput = screen.getByLabelText(/パスワード/i)
    await user.type(passwordInput, 'password123')
    
    // フォーム送信
    const submitButton = screen.getByRole('button', { name: /登録/i })
    await user.click(submitButton)
    
    // 成功メッセージが表示されることを確認
    await waitFor(() => {
      expect(screen.getByText(/登録が完了しました/i)).toBeInTheDocument()
    })
  })
})

