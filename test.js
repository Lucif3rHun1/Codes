function parseJSON(jsonString) {
    try {
        const jsonData = JSON.parse(jsonString);
        const subscriptionData = jsonData.data;

        const activeSubscriptions = subscriptionData.filter(subscription => subscription.attributes.status === 'ACTIVE');

        activeSubscriptions.forEach(subscription => {
            const pricePlanIds = [subscription.relationships.nextPaymentPricePlan.data.id, subscription.relationships.pricePlan.data.id];
            
            pricePlanIds.forEach(pricePlanId => {
                const matchingPricePlan = jsonData.included.find(item => item.type === 'pricePlan' && item.id === pricePlanId);
                if (matchingPricePlan) {
                    console.log(`Status: ACTIVE, Price Plan Title: ${matchingPricePlan.attributes.title}`);
                } else {
                    console.log(`Price plan with ID ${pricePlanId} not found.`);
                }
            });
        });
    } catch (error) {
        console.error('Error parsing JSON:', error);
    }
}

// Example JSON string
const jsonString = `{
    "data" : [ {
        "attributes" : {
          "affiliateMarketing" : null,
          "cancelationAllowed" : false,
          "cancelationDate" : "2021-02-05T01:22:17Z",
          "endDate" : "2021-02-05T01:22:17Z",
          "globalId" : "c5777641-bd67-4d7f-abac-e8ad5e998e95",
          "inFreeTrialNow" : false,
          "meta" : null,
          "minimumTermEndDate" : "2021-01-30T01:07:46Z",
          "nextRenewalDate" : "2021-01-30T01:07:46Z",
          "nextRetryDate" : "2021-02-05T01:19:28Z",
          "pauseCode" : null,
          "pauseDate" : null,
          "pauseReason" : null,
          "pricePlanChangeDate" : null,
          "startDate" : "2021-01-23T01:07:46Z",
          "status" : "TERMINATED",
          "terminationAllowed" : false,
          "transitionAllowed" : false,
          "type" : "PAYING",
          "unsubscribeAllowed" : false,
          "userId" : "USERID:go:7ec8274a-cb68-4e0b-b3f1-c3232d1444d8"
        },
        "id" : "1918157",
        "relationships" : {
          "nextPaymentPricePlan" : {
            "data" : {
              "id" : "3",
              "type" : "pricePlan"
            }
          },
          "paymentMethod" : {
            "data" : {
              "id" : "1905780",
              "type" : "paymentMethod"
            }
          },
          "pricePlan" : {
            "data" : {
              "id" : "3",
              "type" : "pricePlan"
            }
          },
          "product" : {
            "data" : {
              "id" : "1",
              "type" : "product"
            }
          }
        },
        "type" : "subscription"
      }, {
        "attributes" : {
          "affiliateMarketing" : null,
          "cancelationAllowed" : false,
          "cancelationDate" : null,
          "endDate" : null,
          "globalId" : "2f2615e0-55ce-4de4-a533-a5c612579926",
          "inFreeTrialNow" : false,
          "meta" : null,
          "minimumTermEndDate" : "2024-05-12T01:52:00Z",
          "nextRenewalDate" : "2024-05-12T01:52:00Z",
          "nextRetryDate" : null,
          "pauseCode" : null,
          "pauseDate" : null,
          "pauseReason" : null,
          "pricePlanChangeDate" : null,
          "startDate" : "2021-02-05T01:52:18Z",
          "status" : "ACTIVE",
          "terminationAllowed" : false,
          "transitionAllowed" : false,
          "type" : "IAP",
          "unsubscribeAllowed" : false,
          "userId" : "USERID:go:7ec8274a-cb68-4e0b-b3f1-c3232d1444d8"
        },
        "id" : "2901808",
        "relationships" : {
          "nextPaymentPricePlan" : {
            "data" : {
              "id" : "12",
              "type" : "pricePlan"
            }
          },
          "paymentMethod" : {
            "data" : {
              "id" : "2876145",
              "type" : "paymentMethod"
            }
          },
          "pricePlan" : {
            "data" : {
              "id" : "12",
              "type" : "pricePlan"
            }
          },
          "product" : {
            "data" : {
              "id" : "2",
              "type" : "product"
            }
          }
        },
        "type" : "subscription"
      } ],
      "included" : [ {
        "attributes" : {
          "cardExpire" : "2024-04",
          "cardProvider" : "visa",
          "maskedCardNumber" : "9517",
          "paymentType" : "CARD",
          "provider" : "AdyenCheckout",
          "status" : "INVALID"
        },
        "id" : "1905780",
        "relationships" : {
          "postalAddress" : {
            "data" : {
              "id" : "PA:go:b3726082-dae3-45a9-b2b0-7616af15c4b0",
              "type" : "postalAddress"
            }
          }
        },
        "type" : "paymentMethod"
      }, {
        "attributes" : {
          "cardExpire" : null,
          "cardProvider" : null,
          "maskedCardNumber" : null,
          "paymentType" : "IAP",
          "provider" : "Amazon",
          "status" : "VALID"
        },
        "id" : "2876145",
        "type" : "paymentMethod"
      }, {
        "attributes" : {
          "currency" : "USD",
          "currencyDecimalPoints" : 2,
          "customAttributes" : null,
          "endDate" : null,
          "inAppStoreId" : "ad_free_monthly",
          "numberOfInstalments" : 0,
          "numberOfPeriodsBetweenPayments" : 1,
          "numberOfValidPeriods" : null,
          "period" : "MONTH",
          "postponedDays" : 7,
          "price" : 899,
          "provider" : "Amazon",
          "requirePaymentMethod" : false,
          "subscriptionStartDate" : null,
          "title" : "discovery+ (Ad-Free)",
          "type" : "THIRD_PARTY",
          "userFreeTrialStatus" : "UNKNOWN"
        },
        "id" : "12",
        "relationships" : {
          "product" : {
            "data" : {
              "id" : "2",
              "type" : "product"
            }
          }
        },
        "type" : "pricePlan"
      }, {
        "attributes" : {
          "currency" : "USD",
          "currencyDecimalPoints" : 2,
          "customAttributes" : null,
          "endDate" : null,
          "inAppStoreId" : null,
          "numberOfInstalments" : 0,
          "numberOfPeriodsBetweenPayments" : 1,
          "numberOfValidPeriods" : null,
          "period" : "MONTH",
          "postponedDays" : 7,
          "price" : 499,
          "provider" : null,
          "requirePaymentMethod" : true,
          "subscriptionStartDate" : null,
          "title" : "discovery+",
          "type" : "ONGOING",
          "userFreeTrialStatus" : "UNKNOWN"
        },
        "id" : "3",
        "relationships" : {
          "product" : {
            "data" : {
              "id" : "1",
              "type" : "product"
            }
          }
        },
        "type" : "pricePlan"
      } ],
      "meta" : {
        "total" : 2,
        "totalPages" : 1
      }
    }`;

// Call the function with the JSON string
parseJSON(jsonString);
