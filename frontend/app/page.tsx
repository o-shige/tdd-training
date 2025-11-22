export default function Home() {
  return (
    <main style={{ padding: '2rem' }}>
      <h1>Auth TDD Learning</h1>
      <p>JWT認証をTDDで学ぶプロジェクト</p>
      <nav>
        <ul>
          <li><a href="/register">ユーザー登録</a></li>
          <li><a href="/login">ログイン</a></li>
        </ul>
      </nav>
    </main>
  )
}
