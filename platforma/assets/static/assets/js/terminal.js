const fiatOptions = {
    RUB: [
        { value: "TinkoffNew", text: "Tinkoff" },
        { value: "RosBankNew", text: "Rosbank" },
        { value: "RaiffeisenBank", text: "RaiffeisenBank" },
        { value: "QIWI", text: "Qiwi" },
        { value: "BANK", text: "BANK" },
    ],
    USD: [
        { value: "Wise", text: "Wise" },
        { value: "Zelle", text: "Zelle" },
        { value: "WiseInstant", text: "Wise Instant" },
        { value: "AirTM", text: "AirTM" },
    ],
    UZS: [
        { value: "Humo", text: "Humo" },
        { value: "Uzcard", text: "Uzcard" },
        { value: "Anorbank", text: "Anorbank" },
        { value: "IpakYuliBank", text: "Ipak Yuli Bank" },
    ],
    TRY: [
        { value: "Ziraat", text: "Ziraat" },
        { value: "VakifBank", text: "VakifBank" },
        { value: "Garanti", text: "Garanti" },
        { value: "DenizBank", text: "Denizbank" },
        { value: "BANK", text: "BANK" },
    ],
    KGS: [
        { value: "mBank", text: "mBank" },
        { value: "OPTIMABANK", text: "Optima Bank" },
        { value: "DEMIRBANK", text: "DemirBank" },

    ],
    KZT: [
        { value: "KaspiBank", text: "Kaspi Bank" },
        { value: "HalykBank", text: "Halyk Bank" },
        { value: "JysanBank", text: "Jysan Bank" },
        { value: "BANK", text: "BANK" },
    ],
    EUR: [
        { value: "Wise", text: "Wise" },
        { value: "WiseInstant", text: "Wise Instant" },
        { value: "Revolut", text: "Revolut" },
        { value: "BANK", text: "BANK" },
    ],
    CNY: [
        { value: "ALIPAY", text: "Alipay" },
        { value: "WECHAT", text: "WeChat" },
        { value: "BANK", text: "BANK" },
    ],
    GBP: [
        { value: "Wise", text: "Wise" },
        { value: "WiseInstant", text: "Wise Instant" },
        { value: "Revolut", text: "Revolut" },
        { value: "BANK", text: "BANK" },
    ],
    JPY: [
        { value: "LINEPay", text: "LINE pay" },
        { value: "BANK", text: "BANK" },
    ],
    CHF: [
        { value: "FPS", text: "Instant Transfer" },
        { value: "Wise", text: "Wise" },
        { value: "BANK", text: "BANK" },
    ],
    CAD: [
        { value: "InteracETransfer", text: "Interac e-Transfer" },
        { value: "TDbank", text: "TD bank" },
        { value: "CIBCbank", text: "CIBC" },
        { value: "RBCRoyalbank", text: "RBC Royal bank" },
        { value: "BMObank", text: "BMO" },
        { value: "BANK", text: "BANK" },
    ],
    AUD: [
        { value: "Wise", text: "Wise" },
        { value: "Revolut", text: "Revolut" },
        { value: "OKSO", text: "OSKO" },
        { value: "BANK", text: "BANK" },
    ],
    NZD: [
        { value: "Wise", text: "Wise" },
        { value: "BANK", text: "BANK" },
    ],
    };
    const fiatSelect = document.querySelector('select[name="Fiat"]');
    const tradeMethodSelect = document.querySelector(
    'select[name="Trade Method"]'
    );
    function updateTradeMethodOptions() {
    tradeMethodSelect.innerHTML = "";
    const selectedFiat = fiatSelect.value;
    const options = fiatOptions[selectedFiat];
    options.forEach((option) => {
        const optionElement = document.createElement("option");
        optionElement.value = option.value;
        optionElement.text = option.text;
        tradeMethodSelect.appendChild(optionElement);
    });
    }
    fiatSelect.addEventListener("change", () => {
    updateTradeMethodOptions();
    });
    updateTradeMethodOptions();

    function toggleInfo() {
        var checkbox = document.getElementById("myCheckbox");
        var info = document.getElementById("Charts");
        if (checkbox.checked) {
          info.style.display = "block";
          var canvas = document.getElementById("vol");
          canvas.style.display = "block";
          var canvas2 = document.getElementById("vol2");
          canvas2.style.display = "block";
        } else {
          info.style.display = "none";
        }
      }
  