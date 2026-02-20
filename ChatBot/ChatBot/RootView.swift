import SwiftUI

struct RootView: View {
    
    @State private var currentScreen: Screen = .intro
    
    enum Screen {
        case intro
        case history
        case chat
    }
    
    var body: some View {
        switch currentScreen {
        case .intro:
            IntroView(onShowHistory: {
                currentScreen = .history
            })
            
        case .history:
            HistoryView(onShowChat: {
                currentScreen = .chat
            })
            
        case .chat:
            ContentView()
        }
    }
}
