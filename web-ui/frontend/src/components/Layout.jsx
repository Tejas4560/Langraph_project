import Sidebar from './Sidebar'
import Header from './Header'

const Layout = ({ children }) => {
    return (
        <div className="flex min-h-screen">
            <Sidebar />
            <div className="flex-1">
                <Header />
                <main className="p-6">
                    {children}
                </main>
                <footer className="text-center p-6 text-gray-600 border-t mt-8">
                    <p>Built with ❤️ using LangGraph, Groq, React & FastAPI</p>
                    <p className="text-sm mt-1">🚀 Happy Learning!</p>
                </footer>
            </div>
        </div>
    )
}

export default Layout
