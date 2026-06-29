import UIKit
import WebKit

class ViewController: UIViewController, WKUIDelegate {
    var webView: WKWebView!
    
    override func loadView() {
        let webConfiguration = WKWebViewConfiguration()
        // Allow JavaScript and local file access
        webConfiguration.setValue(true, forKey: "allowFileAccessFromFileURLs")
        
        webView = WKWebView(frame: .zero, configuration: webConfiguration)
        webView.uiDelegate = self
        view = webView
    }
    
    override func viewDidLoad() {
        super.viewDidLoad()
        
        // Load the local index.html prototype from iOS app bundle
        if let htmlPath = Bundle.main.path(forResource: "index", ofType: "html", inDirectory: "assets") {
            let htmlURL = URL(fileURLWithPath: htmlPath)
            let directoryURL = htmlURL.deletingLastPathComponent()
            webView.loadFileURL(htmlURL, allowingReadAccessTo: directoryURL)
        } else {
            print("Error: index.html not found in assets directory")
        }
    }
}
