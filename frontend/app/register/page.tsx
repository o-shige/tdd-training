'use client'

import { useState } from 'react'
import { validateRegistrationForm } from './validation'

export default function RegisterPage() {
  const [emailError, setEmailError] = useState('')
  const [passwordError, setPasswordError] = useState('')
  const [successMessage, setSuccessMessage] = useState('')

  const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault()
    const formData = new FormData(e.currentTarget)
    const email = formData.get('email') as string
    const password = formData.get('password') as string
    
    // バリデーション関数を使用
    const validation = validateRegistrationForm(email, password)
    if (!validation.isValid) {
      setEmailError(validation.emailError || '')
      setPasswordError(validation.passwordError || '')
      return
    }
    
    setEmailError('')
    setPasswordError('')
    setSuccessMessage('')
    
    // API呼び出し
    fetch('http://localhost:8000/api/register', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        email,
        password
      })
    })
      .then(async (response) => {
        if (!response.ok) {
          const data = await response.json()
          if (response.status === 409) {
            // 重複メールアドレスエラー
            setEmailError('このメールアドレスは既に登録されています')
          } else {
            // その他のエラー
            setEmailError(data.detail?.error || '登録に失敗しました')
          }
          return
        }
        const data = await response.json()
        // 登録成功時の処理
        setSuccessMessage('登録が完了しました')
        // フォームをリセット
        const form = e.currentTarget
        if (form) {
          form.reset()
        }
      })
      .catch((error) => {
        console.error('エラー:', error)
        setEmailError('ネットワークエラーが発生しました')
      })
  }

  return (
    <div>
      <h1>ユーザー登録</h1>
      <form onSubmit={handleSubmit}>
        <label htmlFor="email">メールアドレス</label>
        <input type="email" id="email" name="email" />
        {emailError && <div>{emailError}</div>}
        <label htmlFor="password">パスワード</label>
        <input type="password" id="password" name="password" />
        {passwordError && <div>{passwordError}</div>}
        {successMessage && <div>{successMessage}</div>}
        <button type="submit">登録</button>
      </form>
    </div>
  )
}

