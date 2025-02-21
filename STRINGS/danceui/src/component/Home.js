import React from "react";
import "./Home.css";

const Home = () => {
	return (
		<section className='slider_section'>
			<div className='carousel'>
				<div className='carousel-item active'>
					<div className='container'>
						<div className='row'>
							{/* Left Side - Text Content */}
							<div className='col-md-6'>
								<div className='detail-box'>
									<h1>
										Crypto <br />
										Currency
									</h1>
									<p>
										Explicabo esse amet tempora quibusdam laudantium, laborum
										eaque magnam fugiat hic? Esse dicta aliquid error
										repudiandae earum suscipit fugiat molestias, veniam, vel
										architecto veritatis delectus repellat modi impedit sequi.
									</p>
									<div className='btn-box'>
										<a
											href='/'
											className='btn1'>
											Read More
										</a>
									</div>
								</div>
							</div>

							{/* Right Side - Image */}
							<div className='col-md-6'>
								<div className='img-box'>
									<img
										src='images/slider-img.png'
										alt='Crypto Currency'
									/>
								</div>
							</div>
						</div>
					</div>
				</div>
			</div>
		</section>
	);
};

export default Home;
