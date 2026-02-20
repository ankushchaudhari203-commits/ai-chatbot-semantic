import Foundation

struct ChatRequest: Codable {
    let session_id: String
    let message: String
}

struct ChatResponse: Codable {
    let reply: String
    let state: String
    let total_price: Double?
    let items: [String]?
}

class APIService {

    static func sendMessage(
        _ message: String,
        sessionID: String,
        completion: @escaping (ChatResponse?) -> Void
    ) {
        guard let url = URL(string: "http://127.0.0.1:8000/chat/") else {
            completion(nil)
            return
        }

        let requestBody = ChatRequest(session_id: sessionID, message: message)

        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")

        do {
            request.httpBody = try JSONEncoder().encode(requestBody)
        } catch {
            completion(nil)
            return
        }

        URLSession.shared.dataTask(with: request) { data, response, error in

            if let error = error {
                print("Network error:", error)
                completion(nil)
                return
            }

            guard let data = data else {
                completion(nil)
                return
            }

            do {
                let decoded = try JSONDecoder().decode(ChatResponse.self, from: data)
                DispatchQueue.main.async {
                    completion(decoded)
                }
            } catch {
                print("Decoding error:", error)
                completion(nil)
            }

        }.resume()
    }
}
