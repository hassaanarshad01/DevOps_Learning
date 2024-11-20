import React from 'react';
import { MDBFooter, MDBContainer, MDBRow, MDBCol, MDBIcon } from 'mdb-react-ui-kit';
import 'mdb-react-ui-kit/dist/css/mdb.min.css';
import '@fortawesome/fontawesome-free/css/all.min.css';

export default function App() {
  return (
    <MDBFooter style={{ backgroundColor: '#0f1235' }} className='text-center text-lg-start text-muted'>
      <section className='d-flex justify-content-center justify-content-lg-between p-4 border-bottom'>
        <div className='me-5 d-none d-lg-block'>
          <span></span>
        </div>

        <div>
          <a href='https://www.instagram.com/hassaanarshad2000/' className='me-4 text-reset'>
            <MDBIcon color='secondary' fab icon='instagram' />
          </a>
          <a href='https://www.linkedin.com/in/hassaan-arshad-196675131' className='me-4 text-reset'>
            <MDBIcon color='secondary' fab icon='linkedin' />
          </a>
          <a href='https://github.com/hassaanarshad01' className='me-4 text-reset'>
            <MDBIcon color='secondary' fab icon='github' />
          </a>
        </div>
      </section>

      <section className=''>
        <MDBContainer className='text-center text-md-start mt-5'>
          <MDBRow className='mt-3'>
            <MDBCol md='3' lg='4' xl='3' className='mx-auto mb-4'>
              <h6 className='text-uppercase fw-bold mb-4'>
                <MDBIcon color='secondary' icon='gem' className='me-3' />
                ReArtify-AI
              </h6>
              <p>
              ReArtify-AI is a final-year R&D project sponsored by the FAST-NUCES Computer Science program and supervised by Dr. Akhtar Jamil.
              </p>
            </MDBCol>

            <MDBCol md='3' lg='2' xl='2' className='mx-auto mb-4'>
              <h6 className='text-uppercase fw-bold mb-4'>Useful links</h6>
              <p>
                <a href='http://isb.nu.edu.pk/' className='text-reset'>
                  University Homepage
                </a>
              </p>
              <p>
                <a href='https://www.linkedin.com/in/hassaan-arshad-196675131' className='text-reset'>
                  LinkedIn - Hassaan Arshad
                </a>
              </p>
              <p>
                <a href='https://www.linkedin.com/in/salahuddin-yousaf-52184527a' className='text-reset'>
                  LinkedIn - Salahuddin Yousuf
                </a>
              </p>
              <p>
                <a href='https://www.linkedin.com/in/fahad-kamran-kundi' className='text-reset'>
                  LinkedIn - Fahad Kamran
                </a>
              </p>
            </MDBCol>

            <MDBCol md='4' lg='3' xl='3' className='mx-auto mb-md-0 mb-4'>
              <h6 className='text-uppercase fw-bold mb-4'>Contact</h6>
              <p>
                <MDBIcon color='secondary' icon='home' className='me-2' />
                FAST University, 3 A.K. Brohi Road, H-11/4 H 11/4 H-11, Islamabad, Islamabad Capital Territory
              </p>
              <p>
                <MDBIcon color='secondary' icon='envelope' className='me-3' />
                i200629@nu.edu.pk
              </p>
              <p>
                <MDBIcon color='secondary' icon='phone' className='me-3' /> +923470102521
              </p>
            </MDBCol>
          </MDBRow>
        </MDBContainer>
      </section>
    </MDBFooter>
  );
}
