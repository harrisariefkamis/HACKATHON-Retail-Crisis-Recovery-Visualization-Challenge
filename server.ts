import express from "express";
import path from "path";
import dotenv from "dotenv";
import { createServer as createViteServer } from "vite";
import { GoogleGenAI, Type } from "@google/genai";

// Initialize dotenv configuration
dotenv.config();

const app = express();
const PORT = 3000;

// Enable JSON bodies up to 10MB (for larger CSV transfers)
app.use(express.json({ limit: "10mb" }));

// Initialize Gemini SDK with telemetry header
const apiKey = process.env.GEMINI_API_KEY || "";
let ai: GoogleGenAI | null = null;
if (apiKey) {
  ai = new GoogleGenAI({
    apiKey: apiKey,
    httpOptions: {
      headers: {
        "User-Agent": "aistudio-build",
      },
    },
  });
}

// 1. API Endpoint for Sales & Association Rules Insights powered by Gemini
app.post("/api/analyze", async (req, res) => {
  try {
    const { targetLabel, summary, topRules } = req.body;

    if (!summary) {
      return res.status(400).json({
        success: false,
        error: "Missing parameters. 'summary' object is required.",
      });
    }

    if (!ai) {
      return res.json({
        success: true,
        executiveSummary: "AI Consultant is currently offline. Please configure your GEMINI_API_KEY to activate senior analyst advice.",
        strategicAdvice: "Ensure your store tracks products accurately and focuses on products with high-frequency streaks. For coffee setups, keep items fresh and monitor daily MA levels.",
        bundleIdeas: "Suggested core bundle: Combine key high-demand pairs (like coffee beans and filter papers) at an attractive bundle price (e.g., 5-10% off) to increase average receipt values.",
      });
    }

    // Construct precise prompt with Indonesian coffee shop retail context
    const rulesStr = topRules && topRules.length > 0 
      ? topRules.slice(0, 5).map((r: any, idx: number) => 
          `${idx + 1}. JIKA membeli [${r.antecedents.join(", ")}] MAKA membeli [${r.consequents.join(", ")}] (Invoices: ${r.invoiceCount}, Support: ${(r.support*100).toFixed(1)}%, Confidence: ${(r.confidence*100).toFixed(1)}%, Lift: ${r.lift.toFixed(2)})`
        ).join("\n")
      : "Tidak ditemukan aturan asosiasi yang signifikan (Lift > 1.0) dengan support min 1%.";

    const prompt = `Anda adalah Senior Retail Consultant & Business Strategic Analyst ahli dalam pasar retail kopi/cafe di Indonesia.
Menganalisis performa toko berdasarkan metrik berikut:
- Target Produk Fokus: "${targetLabel}"
- Rekor Kenaikan Tren Berturut-turut: ${summary.rekorKenaikan} hari (puncak pada tanggal ${summary.rekorTanggal})
- Total Nilai Pendapatan Toko: Rp ${summary.totalRevenue.toLocaleString("id-ID")}
- Total Jumlah Invoice: ${summary.totalTransactions} transaksi
- Variasi Produk Unik: ${summary.uniqueProducts.join(", ")}
- Aturan Asosiasi Market Basket Analysis (Top 5 Rules):
${rulesStr}

Tugas Anda adalah memformulasikan wawasan eksekutif, saran strategis fluktuasi/tren, dan rekomendasi program bundling promosi yang kreatif dan menguntungkan.
Respons HARUS berupa JSON object terstruktur sesuai schema yang disediakan. Gunakan bahasa Indonesia yang santun, profesional, tajam, dan edukatif untuk pemilik usaha retail.`;

    // Local High-Fidelity Indonesian Fallback Generator
    const getIndonesianFallback = () => {
      const rekorKenaikan = summary.rekorKenaikan || 0;
      const rekorTanggal = summary.rekorTanggal || "N/A";
      const totalRevenue = summary.totalRevenue || 0;
      const totalTransactions = summary.totalTransactions || 0;
      const uniqueProducts = summary.uniqueProducts || [];
      const formattedRevenue = `Rp ${totalRevenue.toLocaleString("id-ID")}`;

      const executiveSummary = `Berdasarkan tinjauan data transaksi, toko Anda menunjukkan kinerja operasional yang solid dengan total pendapatan mencapai ${formattedRevenue} sepanjang ${totalTransactions} transaksi. Fokus analisis pada produk "${targetLabel}" mencatatkan rekor kenaikan penjualan berturut-turut selama ${rekorKenaikan} hari (puncak penjualan pada ${rekorTanggal}).

Pemberian perhatian khusus pada tren harian "${targetLabel}" mengindikasikan adanya momentum pembelian pelanggan yang kuat. Kenaikan berturut-turut ini mengonfirmasi bahwa produk ini bertindak sebagai "traffic generator" utama. Analisis pola keranjang belanja (Market Basket Analysis) juga menunjukkan korelasi positif yang kuat antar produk pendukung, menandakan peluang cross-selling yang sangat tinggi di masa mendatang.`;

      const strategicAdvice = `Menyikapi rekor kenaikan ${rekorKenaikan} hari beruntun untuk produk "${targetLabel}", berikut langkah taktis yang direkomendasikan untuk mengantisipasi normalisasi permintaan (trend cooling-off):

1. **Manajemen Pengadaan Stok Efisien**: Jaga level stok bahan baku "${targetLabel}" agar tidak mengalami "out-of-stock" (OOS) di masa puncak, namun hindari tumpukan stok berlebih (overstocking) saat grafik melandai dengan terus mengacu pada Moving Average 3-Hari.
2. **Standardisasi Layanan**: Kecepatan pemrosesan transaksi harus konsisten tinggi selama periode puncak harian untuk memelihara kepuasan pelanggan.
3. **Pemanfaatan Hari Puncak**: Tingkatkan stok persiapan pada H-1 tanggal historis puncak yaitu sekitar ${rekorTanggal} guna memaksimalkan volume penjualan tanpa kendala operasional.`;

      let bundleIdeas = `Program promosi bundling kreatif berbasis hasil Market Basket Analysis dirancang untuk meningkatkan ukuran keranjang belanja (Average Basket Size):\n\n`;

      if (topRules && topRules.length > 0) {
        topRules.slice(0, 3).forEach((rule: any, idx: number) => {
          const ante = rule.antecedents.join(" & ");
          const cons = rule.consequents.join(" & ");
          const confidencePercent = ((rule.confidence || 0) * 100).toFixed(0);
          const liftVal = (rule.lift || 1).toFixed(2);
          
          bundleIdeas += `${idx + 1}. **Paket Sinergi Korelatif (Beli ${ante} + ${cons})**: Terinspirasi dari aturan asosiasi terkuat dengan Lift Score ${liftVal} dan Confidence ${confidencePercent}%. Tawarkan diskon bundling sebesar 10-15% bagi pelanggan yang membeli kombinasi item ini secara langsung.\n`;
        });
      } else {
        bundleIdeas += `1. **Paket Teman Setia (${targetLabel} Premium Pair)**: Padukan produk utama "${targetLabel}" dengan produk komplementer terpopuler dengan harga komoditas (misal: camilan pendamping atau aksesoris filter). Berikan potongan harga 10% untuk pembelian paket.\n2. **Paket Jam Sibuk (Happy Hour Combo)**: Tawarkan harga promo khusus pada jam-jam lesu guna mendistribusikan pola kedatangan pelanggan secara lebih merata sepanjang hari kerja.\n`;
      }
      
      bundleIdeas += `\n*Rekomendasi Penempatan Rak (Cross-Merchandising)*: Letakkan barang pelengkap yang memiliki korelasi kuat di dekat kasir atau bersebelahan langsung dengan etalase "${targetLabel}" untuk memicu impuls buying.`;

      return {
        executiveSummary,
        strategicAdvice,
        bundleIdeas,
      };
    };

    let responseText = "";

    // Try primary model: gemini-3.5-flash
    try {
      const response = await ai.models.generateContent({
        model: "gemini-3.5-flash",
        contents: prompt,
        config: {
          systemInstruction: "Anda adalah analis data retail senior yang menguasai taktik logistik, penempatan rak barang (shelf placement), cross-selling, dan kampanye bundle promosi di Indonesia.",
          responseMimeType: "application/json",
          responseSchema: {
            type: Type.OBJECT,
            required: ["executiveSummary", "strategicAdvice", "bundleIdeas"],
            properties: {
              executiveSummary: {
                type: Type.STRING,
                description: "Review performa toko keseluruhan, interpretasi rekor berturut-turut fokus produk, dan ulasan pola pembeli dalam bahasa Indonesia.",
              },
              strategicAdvice: {
                type: Type.STRING,
                description: "Saran taktis mengantisipasi penurunan sehabis kenaikan tren berturut-turut, penataan stok, dan mitigasi logistik.",
              },
              bundleIdeas: {
                type: Type.STRING,
                description: "Saran program bundling diskon kreatif bersasarkan Market Basket Analysis dan penempatan barang yang berdampingan (cross-merchandising).",
              },
            },
          },
        },
      });
      responseText = response.text || "";
    } catch (primaryErr: any) {
      console.warn("Primary model 'gemini-3.5-flash' failed or UNAVAILABLE, trying fallback model 'gemini-3.1-flash-lite'...", primaryErr);
      
      // Try fallback model: gemini-3.1-flash-lite
      try {
        const response = await ai.models.generateContent({
          model: "gemini-3.1-flash-lite",
          contents: prompt,
          config: {
            systemInstruction: "Anda adalah analis data retail senior yang menguasai taktik logistik, penempatan rak barang (shelf placement), cross-selling, dan kampanye bundle promosi di Indonesia.",
            responseMimeType: "application/json",
            responseSchema: {
              type: Type.OBJECT,
              required: ["executiveSummary", "strategicAdvice", "bundleIdeas"],
              properties: {
                executiveSummary: { type: Type.STRING },
                strategicAdvice: { type: Type.STRING },
                bundleIdeas: { type: Type.STRING },
              },
            },
          },
        });
        responseText = response.text || "";
      } catch (fallbackErr: any) {
        console.error("All Gemini API models returned errors. Activating dynamic local high-fidelity advisor.", fallbackErr);
      }
    }

    if (responseText) {
      try {
        const parsedResponse = JSON.parse(responseText);
        return res.json({
          success: true,
          ...parsedResponse,
        });
      } catch (parseErr) {
        console.error("Failed to parse Gemini response JSON.", parseErr);
      }
    }

    // Fallback response when both models fail
    const fallbackResults = getIndonesianFallback();
    res.json({
      success: true,
      ...fallbackResults,
      note: "Mengaktifkan Advisor Analis Lokal tingkat tinggi karena kesibukan pelayanan Server AI (503/UNAVAILABLE)."
    });
  } catch (error: any) {
    console.error("Endpoint process error:", error);
    res.status(500).json({
      success: false,
      error: error.message || "Terjadi kesalahan internal ketika memproses analisis AI.",
    });
  }
});

// Serve public static files directly (Vite handles this in development)
// Vite middleware setup
async function setupServer() {
  if (process.env.NODE_ENV !== "production") {
    // Development configuration
    console.log("Starting server in DEVELOPMENT mode...");
    const vite = await createViteServer({
      server: { middlewareMode: true },
      appType: "spa",
    });
    app.use(vite.middlewares);
  } else {
    // Production configuration
    console.log("Starting server in PRODUCTION mode...");
    const distPath = path.join(process.cwd(), "dist");
    app.use(express.static(distPath));
    
    // Serve index.html for any remaining SPA route requests
    app.get("*", (req, res) => {
      res.sendFile(path.join(distPath, "index.html"));
    });
  }

  app.listen(PORT, "0.0.0.0", () => {
    console.log(`Express server running at http://0.0.0.0:${PORT}`);
  });
}

setupServer();
