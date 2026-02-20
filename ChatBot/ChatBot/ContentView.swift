import SwiftUI

struct ChatMessage: Identifiable {
    let id = UUID()
    let text: String
}

struct ContentView: View {

    @State private var userInput = ""
    @State private var messages: [ChatMessage] = []
    @State private var sessionID = UUID().uuidString

    @State private var totalPrice: Double = 0.0
    @State private var orderItems: [String] = []
    @State private var showCheckout = false

    var body: some View {
        VStack {

            ScrollView {
                VStack(spacing: 16) {
                    ForEach(messages) { message in
                        HStack {
                            if message.text.starts(with: "You:") {

                                Spacer()

                                Text(message.text.replacingOccurrences(of: "You: ", with: ""))
                                    .padding()
                                    .background(Color.blue)
                                    .foregroundColor(.white)
                                    .cornerRadius(12)

                            } else {

                                Text(message.text.replacingOccurrences(of: "Bot: ", with: ""))
                                    .padding()
                                    .background(Color.gray.opacity(0.2))
                                    .cornerRadius(12)

                                Spacer()
                            }
                        }
                    }
                }
                .padding()
            }

            Divider()

            HStack {
                TextField("Type message...", text: $userInput)
                    .textFieldStyle(RoundedBorderTextFieldStyle())
                    .onSubmit {
                        sendMessage()
                    }

                Button("Send") {
                    sendMessage()
                }
                .padding(.horizontal)
            }
            .padding()
        }
        .sheet(isPresented: $showCheckout) {
            CheckoutView(items: orderItems, total: totalPrice)
        }
    }

    func sendMessage() {

        guard !userInput.isEmpty else { return }

        let message = userInput
        messages.append(ChatMessage(text: "You: \(message)"))
        userInput = ""

        APIService.sendMessage(message, sessionID: sessionID) { response in

            if let response = response {

                messages.append(ChatMessage(text: "Bot: \(response.reply)"))

                if let price = response.total_price {
                    totalPrice = price
                }

                if let items = response.items {
                    orderItems = items
                }

                // Detect checkout state
                if response.state.uppercased() == "CHECKOUT" {
                    showCheckout = true
                }

            } else {
                messages.append(ChatMessage(text: "Bot: Error"))
            }
        }
    }
}
