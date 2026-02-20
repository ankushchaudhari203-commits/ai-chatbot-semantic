import SwiftUI

struct HistoryView: View {
    
    var onShowChat: () -> Void
    
    var body: some View {
        VStack {
            
            Text("The Story of Pizza 🍕")
                .font(.largeTitle)
                .fontWeight(.bold)
                .padding(.top, 20)
            
            ScrollView {
                Text("""
Pizza originated in Naples, Italy in the 18th century.

It was initially a simple dish for the working class — flatbread topped with tomatoes, cheese, olive oil, and herbs.

The famous Margherita pizza was created in 1889 and named after Queen Margherita of Italy.

Today, pizza is one of the most loved dishes worldwide, evolving into countless variations.

Welcome to Pizzeria — where tradition meets AI.
""")
                .font(.body)
                .padding()
            }
            
            Spacer()
            
            Button("Start Ordering 🍕") {
                onShowChat()
            }
            .padding()
        }
        .padding()
    }
}
