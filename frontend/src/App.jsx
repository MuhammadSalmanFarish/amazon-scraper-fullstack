import axios from "axios"
import { useState } from "react"
import { useNavigate } from "react-router-dom";
import "./App.css"
import toast,{Toaster} from "react-hot-toast"






export default function App(){
  const [product,setProduct] = useState("")
  const [loading,setLoading] = useState(false)
  const navigate = useNavigate()

  const HandleScrape = async()=>{
      if(!product){
        toast.error("Enter a product name")
        return
      }

      const loadingToast=toast.loading("Scraping Started")
      setLoading(true)
      try{
      const response = await axios.post("http://127.0.0.1:5000/scrape",{product:product})
      toast.dismiss(loadingToast)
      toast.success(response.data.message)
      localStorage.setItem("last_product",product)
      setProduct("")
      navigate("/dashboard")
      }
      catch{
        toast.dismiss(loadingToast)
        toast.error("An error occured")
      }
      
      setLoading(false)
      
  }
  
  return <div id="home-page">
           
            <input 
            type="text" 
            placeholder="Enter product name" 
            value={product} 
            onChange={(e)=>setProduct(e.target.value)}></input>
            
            <button onClick={HandleScrape} disabled={loading}>{loading? <div className="loader"></div>:"Scrape"}</button>

           


            <div id="box">
              
            </div>

            <div id="project-desc">
                <h1>Amazon Web Scraper</h1>
                <p>A complete full-stack solution demonstrating Python scraping, API development, React UI, and database integration</p>
            </div>

            <Toaster position="top-center"/>

          </div>

 
}