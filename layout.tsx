export const metadata = {
  title: 'Arabic Code Auditor Pro',
  description: 'منصة فحص الأكواد العربية',
};

export default function RootLayout({ children }) {
  return (
    <html lang="ar" dir="rtl">
      <body>{children}</body>
    </html>
  );
}
