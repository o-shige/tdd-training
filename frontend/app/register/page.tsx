export default function RegisterPage() {
  return (
    <div>
      <h1>ユーザー登録</h1>
      <form>
        <label htmlFor="email">メールアドレス</label>
        <input type="email" id="email" name="email" />
        <label htmlFor="password">パスワード</label>
        <input type="password" id="password" name="password" />
      </form>
    </div>
  )
}

