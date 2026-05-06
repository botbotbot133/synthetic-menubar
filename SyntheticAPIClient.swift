import Foundation
import Combine

struct QuotaResponse: Codable {
    let creditsRemaining: Int
    let creditsUsedToday: Int
    let monthlyLimit: Int
    let lastUpdated: Date
    
    enum CodingKeys: String, CodingKey {
        case creditsRemaining = "credits_remaining"
        case creditsUsedToday = "credits_used_today"
        case monthlyLimit = "monthly_limit"
        case lastUpdated = "last_updated"
    }
}

class SyntheticAPIClient: ObservableObject {
    @Published var lastResponse: QuotaResponse?
    var refreshTrigger = PassthroughSubject<Void, Never>()
    private var cancellables = Set<AnyCancellable>()
    
    init() {
        refreshTrigger
            .flatMap { self.fetchQuotas() }
            .sink(receiveCompletion: { _ in }, receiveValue: { [weak self] response in
                self?.lastResponse = response
            })
            .store(in: &cancellables)
    }
    
    func fetchQuotas() -> AnyPublisher<QuotaResponse, Error> {
        guard let apiKey = UserDefaults.standard.string(forKey: "apiKey"), !apiKey.isEmpty else {
            return Fail(error: APIError.noAPIKey).eraseToAnyPublisher()
        }
        
        guard let url = URL(string: "https://api.synthetic.new/openai/v1/quotas") else {
            return Fail(error: APIError.invalidURL).eraseToAnyPublisher()
        }
        
        var request = URLRequest(url: url)
        request.setValue("Bearer \(apiKey)", forHTTPHeaderField: "Authorization")
        request.setValue("application/json", forHTTPHeaderField: "Accept")
        
        return URLSession.shared.dataTaskPublisher(for: request)
            .tryMap { data, response -> Data in
                guard let httpResponse = response as? HTTPURLResponse else {
                    throw APIError.unknown
                }
                
                switch httpResponse.statusCode {
                case 200:
                    return data
                case 401:
                    throw APIError.unauthorized
                case 429:
                    throw APIError.rateLimited
                default:
                    throw APIError.serverError(httpResponse.statusCode)
                }
            }
            .decode(type: QuotaResponse.self, decoder: JSONDecoder())
            .map { response in
                var mutableResponse = response
                mutableResponse = QuotaResponse(
                    creditsRemaining: response.creditsRemaining,
                    creditsUsedToday: response.creditsUsedToday,
                    monthlyLimit: response.monthlyLimit,
                    lastUpdated: Date()
                )
                return mutableResponse
            }
            .eraseToAnyPublisher()
    }
}

enum APIError: Error {
    case noAPIKey
    case invalidURL
    case unauthorized
    case rateLimited
    case serverError(Int)
    case unknown
}

extension APIError: LocalizedError {
    var errorDescription: String? {
        switch self {
        case .noAPIKey:
            return "No API key configured. Please set your Synthetic API key in settings."
        case .invalidURL:
            return "Invalid API URL"
        case .unauthorized:
            return "Unauthorized. Please check your API key."
        case .rateLimited:
            return "Rate limited. Please wait before retrying."
        case .serverError(let code):
            return "Server error: \(code)"
        case .unknown:
            return "Unknown error occurred"
        }
    }
}
