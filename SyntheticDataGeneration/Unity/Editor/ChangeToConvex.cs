using UnityEditor;
using UnityEngine;

namespace Project.Editor
{
   
    public class ChangeToConvex
    {
        [MenuItem("Elisar/Debug")]
        public static void Cahnge()
        {
            GameObject[] allObjects = UnityEngine.Object.FindObjectsOfType<GameObject>() ;
            foreach(GameObject go in allObjects)
                if (go.GetComponent<MeshCollider>())
                {
                    go.GetComponent<MeshCollider>().convex = true;
                    Debug.Log("Convexed!");
                }

        }
            
    }
}