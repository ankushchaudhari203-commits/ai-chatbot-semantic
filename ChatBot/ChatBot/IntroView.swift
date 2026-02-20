import SwiftUI

struct IntroView: View {
    
    var onShowHistory: () -> Void
    
    @State private var isChecked = false
    @State private var isHovering = false
    
    var body: some View {
        VStack {
            
            Spacer()
            
            Image("pizza")
                .resizable()
                .scaledToFit()
                .frame(width: 140, height: 140)
            
            Text("Welcome to Pizzeria")
                .font(.largeTitle)
                .fontWeight(.bold)
                .padding(.top, 20)
            
            Spacer()
            
            Toggle(isOn: $isChecked) {
                Text("This is a Minimalistic chat bot for ordering pizza, please tick the box and click proceed further")
                    .font(.callout)
            }
            .toggleStyle(.checkbox)
            .padding(.horizontal, 40)
            
            HStack {
                Spacer()
                
                Button(action: {
                    onShowHistory()
                }) {
                    Text("Next")
                        .foregroundColor(.white)
                        .padding(.horizontal, 24)
                        .padding(.vertical, 10)
                        .background(isHovering ? Color.blue.opacity(0.7) : Color.blue)
                        .cornerRadius(8)
                }
                .disabled(!isChecked)
                .onHover { hovering in
                    isHovering = hovering
                }
                .padding()
            }
        }
        .padding()
    }
}


