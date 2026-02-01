import { useState,useEffect } from "react"
import axios from "axios"
import "./dashboard.css"
import { Link } from "react-router-dom"

export default function Dashboard(){
        const product_name = localStorage.getItem("last_product")
        const [products,setProduct] = useState([])

        useEffect(()=>{
            fetchproduct()
            document.title="Dashboard"
        },[])

        const fetchproduct =async ()=>{
            const res = await axios.get("http://127.0.0.1:5000/products")
            setProduct(res.data)
        }
    return <div id="main-product-div">
                <header><h1>PRODUCTS DASHBOARD</h1></header>
                <div id="summary"><h2>Showing results for:{product_name}</h2> <button onClick={()=>window.location.href="http://127.0.0.1:5000/download"}>Download</button></div>
                
                <div id="table-container">
                <table border={1} rules="all">
                    <thead>
                    <tr>
                        <th>Title</th>
                        <th>Price</th>
                        <th>Rating</th>
                        <th>Rating count</th>
                        <th>Link</th>
                    </tr>
                    </thead>
                    
                    <tbody>
                        {products.map((p,index)=>(
                            <tr key={index}>
                                <td>{p.title}</td>
                                <td>{p.price}</td>
                                <td>{p.rating}</td>
                                <td>{p.rating_count}</td>
                                <td><Link to={p.link} target="_blank">Click Here</Link></td>
                            </tr>
                        ))}
                    </tbody>

                </table>
                </div>
        </div>
}