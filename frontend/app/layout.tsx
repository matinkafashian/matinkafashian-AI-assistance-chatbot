import type { Metadata } from 'next'
import { Inter, Vazirmatn } from 'next/font/google'
import './globals.css'

const inter = Inter({ subsets: ['latin'] })
const vazirmatn = Vazirmatn({ subsets: ['arabic'], weight: ['200', '400'] })

export const metadata: Metadata = {
  title: 'AI Chatbot - Python & AI Training Assistant',
  description: 'Intelligent chatbot for Python and Artificial Intelligence training courses by Matin Kafashian',
  keywords: 'Python, AI, Artificial Intelligence, Machine Learning, Programming, Training, Chatbot',
  authors: [{ name: 'Matin Kafashian' }],
  viewport: 'width=device-width, initial-scale=1',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en" dir="ltr">
      <body className={`${inter.className} ${vazirmatn.className}`}>
        {children}
      </body>
    </html>
  )
}
