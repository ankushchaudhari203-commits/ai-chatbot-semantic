import SwiftUI

struct CheckoutView: View {

    var items: [String]
    var total: Double

    @Environment(\.dismiss) var dismiss

    var body: some View {
        VStack(spacing: 20) {

            Text("Order Summary 🍕")
                .font(.largeTitle)
                .fontWeight(.bold)

            List(items, id: \.self) { item in
                Text(item)
            }
            .frame(height: 200)

            Text("Total: $\(String(format: "%.2f", total))")
                .font(.title2)
                .fontWeight(.semibold)

            Button("OK") {
                dismiss()
            }
            .padding()
            .frame(width: 120)
            .background(Color.blue)
            .foregroundColor(.white)
            .cornerRadius(10)

        }
        .padding()
        .frame(width: 400, height: 400)
    }
}
