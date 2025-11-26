'use client'

import { useState } from 'react'

export default function RegisterPage() {
  const [emailError, setEmailError] = useState('')

  const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault()
    const formData = new FormData(e.currentTarget)
    const email = formData.get('email') as string
    
    if (!email || email.trim() === '') {
      setEmailError('メールアドレスは必須です')
      return
    }
    
    setEmailError('')
    // TODO: API呼び出し
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
        <button type="submit">登録</button>
      </form>
    </div>
  )
}

