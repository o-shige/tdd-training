export const metadata = {
  title: 'Auth TDD Learning',
  description: 'JWT認証をTDDで学ぶプロジェクト',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="ja">
      <body>{children}</body>
    </html>
  )
}
