$(document).ready(function () {

    $("#payWithRazorpay").click(function (e) {
        console.log("checkout.js loaded successfull");
        console.log("im g=here");
        e.preventDefault();

        var first_name = $("[name='first_name']").val();
        var last_name = $("[name='last_name']").val();
        var email = $("[name='email']").val();
        var address = $("[name='addressSelected']").val();
        var phone = $("[name='phone']").val();
        var address_line_1 = $("[name='address_line_1']").val();
        var address_line_2 = $("[name='address_line_2']").val();
        var city = $("[name='city']").val();
        var state = $("[name='state']").val();
        var zip_code = $("[name='zip_code']").val();
        var token = $("[name='csrfmiddlewaretoken']").val();
        var grand_total = $("[name='grand_total']").val();
        var couponCode = $("[name='couponCode']").val();
        var couponDiscount = $("[name='couponDiscount']").val();
        var amountToBePaid = $("[name='amountToBePaid']").val();
      
        console.log(first_name,last_name,email,phone,address_line_1,city,state,zip_code);


        if (
            first_name == "" ||
            last_name == "" ||
            email == "" ||
            phone == "" ||
            address_line_1 == "" ||
            address_line_2 == "" ||
            city == "" ||
            state == "" ||
            zip_code == "" 

        ) {
            swal("alert", "All fields are mandatory", "error");
            return false;
        } else {
            console.log("im in else");

            
            $.ajax({

                method: "GET",
                url: "/cart/proceed_to_pay/",
                contentType: "application/json",
                success: function (response) {
                    console.log("im in hell");

                    console.log(response, amountToBePaid);
                    var options = {
                        key: HomeHaven.settings.API_KEY,// Enter the Key ID generated from the Dashboard
                        // amount: 10000,
                        amount: response.amountToBePaid * 100, //response.total_price *100 , // Amount is in currency subunits. Default currency is INR. Hence, 50000 refers to 50000 paise
                        currency: "INR",
                        name: "Hanan V C",
                        description: "Thank you",
                        // image: "",
                        handler: function (responseb) {
                            // alert(responseb.razorpay_payment_id);
                            console.log("56556565");
                            data = {
                                'first_name': first_name,
                                'last_name': last_name,
                                'email': email,
                                'phone': phone,
                                'address_line_1': address_line_1,
                                'address_line_2': address_line_2,
                                'city': city,
                                'state': state,
                                'addressSelected': address,
                                'zip_code': zip_code,
                                'payment_method': "Paid by Razorpay",
                                'payment_id': responseb.razorpay_payment_id,
                                'csrfmiddlewaretoken': token,
                                'amountToBePaid': amountToBePaid,
                                'couponCode': couponCode,
                                'couponDiscount': couponDiscount,
                                'grand_total': grand_total

                            };
                            console.log(grand_total,'total-----------------')
                            $.ajax({
                                method: "POST",
                                url: "/cart/place_order/",
                                data: data,
                                success: function (responsec) {
                                    // var ordernumber = responsec.ordernumber
                                    // console.log(ordernumber)
                                    console.log("heoeo-----------------fff----------")
                                    swal("Congratulations!", responsec.status, "success").then(
                                        (value)=> {
                                            window.location.href ="/cart/order-complete/" + responsec.ordernumber + "/" ;
                                                
                                        }
                                    );

                                },
                            });
                            console.log("check");
                        },
                        prefill: {

                            email: email,
                            contact: phone,
                        },
                        notes: {
                            address: "HomeHaven India Pvt Ltd",
                        },
                        theme: {
                            color: "#3399cc",
                        },
                    };
                    var rzp1 = new Razorpay(options);
                    rzp1.open();
                },
            });
        }
    });
})