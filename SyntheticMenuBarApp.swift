import SwiftUI
import Combine

@main
struct SyntheticMenuBarApp: App {
    @NSApplicationDelegateAdaptor(AppDelegate.self) var appDelegate
    
    var body: some Scene {
        Settings {
            SettingsView()
        }
    }
}

class AppDelegate: NSObject, NSApplicationDelegate {
    var statusItem: NSStatusItem?
    var popover: NSPopover?
    var apiClient = SyntheticAPIClient()
    var cancellables = Set<AnyCancellable>()
    var timer: Timer?
    
    func applicationDidFinishLaunching(_ notification: Notification) {
        // Create status bar item
        statusItem = NSStatusBar.shared.statusItem(withLength: NSStatusItem.variableLength)
        
        if let button = statusItem?.button {
            button.image = NSImage(systemSymbolName: "creditcard", accessibilityDescription: "Synthetic Credits")
            button.title = "Loading..."
            button.action = #selector(togglePopover)
            button.target = self
        }
        
        // Create popover
        popover = NSPopover()
        popover?.contentSize = NSSize(width: 300, height: 200)
        popover?.behavior = .transient
        popover?.contentViewController = NSHostingController(rootView: ContentView(apiClient: apiClient))
        
        // Initial fetch
        fetchCredits()
        
        // Auto-refresh every 5 minutes
        timer = Timer.scheduledTimer(withTimeInterval: 300, repeats: true) { _ in
            self.fetchCredits()
        }
    }
    
    @objc func togglePopover() {
        if let button = statusItem?.button {
            if popover?.isShown == true {
                popover?.performClose(nil)
            } else {
                popover?.show(relativeTo: button.bounds, of: button, preferredEdge: .minY)
            }
        }
    }
    
    func fetchCredits() {
        apiClient.fetchCredits()
            .receive(on: DispatchQueue.main)
            .sink { completion in
                if case .failure(let error) = completion {
                    self.statusItem?.button?.title = "❌"
                    print("Error fetching credits: \(error)")
                }
            } receiveValue: { response in
                let remaining = response.creditsRemaining
                self.statusItem?.button?.title = "\(remaining)"
            }
            .store(in: &cancellables)
    }
}

struct ContentView: View {
    @ObservedObject var apiClient: SyntheticAPIClient
    
    var body: some View {
        VStack(spacing: 16) {
            if let response = apiClient.lastResponse {
                VStack(alignment: .leading, spacing: 8) {
                    HStack {
                        Text("Credits:")
                            .fontWeight(.bold)
                        Spacer()
                        Text("\(response.creditsRemaining)")
                            .foregroundColor(response.creditsRemaining < 100 ? .red : .green)
                    }
                    
                    HStack {
                        Text("Used Today:")
                        Spacer()
                        Text("\(response.creditsUsedToday)")
                    }
                    
                    HStack {
                        Text("Monthly Limit:")
                        Spacer()
                        Text("\(response.monthlyLimit)")
                    }
                    
                    Divider()
                    
                    Text("Last updated: \(response.lastUpdated, style: .time)")
                        .font(.caption)
                        .foregroundColor(.secondary)
                }
                .padding()
            } else {
                Text("Loading...")
                    .foregroundColor(.secondary)
            }
            
            Button("Refresh Now") {
                apiClient.refreshTrigger.send()
            }
            .padding(.horizontal)
            
            Button("Open Settings") {
                NSApp.sendAction(Selector(("showSettingsWindow:")), to: nil, from: nil)
            }
            .padding(.horizontal)
            
            Divider()
            
            Button("Quit") {
                NSApplication.shared.terminate(nil)
            }
            .padding(.horizontal)
        }
        .frame(width: 280)
        .padding()
    }
}

struct SettingsView: View {
    @AppStorage("apiKey") private var apiKey: String = ""
    @AppStorage("refreshInterval") private var refreshInterval: Double = 300
    
    var body: some View {
        Form {
            Section("API Configuration") {
                SecureField("API Key", text: $apiKey)
                    .textFieldStyle(RoundedBorderTextFieldStyle())
                
                Text("Your Synthetic API key")
                    .font(.caption)
                    .foregroundColor(.secondary)
            }
            
            Section("Settings") {
                Picker("Refresh Interval", selection: $refreshInterval) {
                    Text("1 minute").tag(60.0)
                    Text("5 minutes").tag(300.0)
                    Text("15 minutes").tag(900.0)
                    Text("30 minutes").tag(1800.0)
                }
            }
            
            Section {
                Button("Save") {
                    // Settings are auto-saved via @AppStorage
                    NSApp.sendAction(Selector(("showMainWindow:")), to: nil, from: nil)
                }
            }
        }
        .padding()
        .frame(width: 400, height: 250)
    }
}
